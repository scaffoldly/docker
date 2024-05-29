import { APIGatewayProxyResultV2 } from "aws-lambda";
import axios, { AxiosResponseHeaders, RawAxiosResponseHeaders } from "axios";
import net from "net";
import { EndpointRequest, EndpointResponse } from "./types";

function convertHeaders(
  headers: RawAxiosResponseHeaders | AxiosResponseHeaders
): { [header: string]: boolean | number | string } | undefined {
  if (!headers) {
    return undefined;
  }

  return Object.keys(headers).reduce((acc, key) => {
    const value = headers[key];

    if (!value) return acc;

    if (Array.isArray(value)) {
      acc[key] = value.join(", ");
    } else if (
      typeof value === "string" ||
      typeof value === "number" ||
      typeof value === "boolean"
    ) {
      acc[key] = value;
    }

    return acc;
  }, {} as { [header: string]: boolean | number | string });
}

const waitForEndpoint = async (
  endpoint: string,
  deadline: number
): Promise<{ deadline: number }> => {
  const start = Date.now();
  const url = new URL(endpoint);
  const hostname = url.hostname;
  const port = parseInt(url.port, 10) || (url.protocol === "https:" ? 443 : 80);

  return new Promise((resolve) => {
    const socket = new net.Socket();

    const onError = () => {
      socket.destroy();
      return waitForEndpoint(endpoint, deadline - (Date.now() - start)).then(
        resolve
      );
    };

    socket.setTimeout(deadline);
    socket.once("error", onError);
    socket.once("timeout", onError);

    socket.connect(port, hostname, () => {
      socket.end();
      resolve({ deadline: deadline - (Date.now() - start) });
    });
  });
};

export const endpointProxy = async ({
  requestId,
  endpoint,
  event,
  initialDeadline,
}: EndpointRequest): Promise<EndpointResponse> => {
  const {
    requestContext,
    rawPath,
    rawQueryString,
    headers: rawHeaders,
    body: rawBody,
    isBase64Encoded,
  } = event;
  const method = requestContext.http.method;

  const { deadline } = await waitForEndpoint(endpoint, initialDeadline);

  if (deadline <= 0) {
    throw new Error(
      `${endpoint.toString()} took longer than ${Math.floor(
        initialDeadline / 1000
      )} second(s) to start.`
    );
  }

  const url = new URL(rawPath, endpoint);
  if (rawQueryString) {
    url.search = new URLSearchParams(rawQueryString).toString();
  }

  const decodedBody =
    isBase64Encoded && rawBody ? Buffer.from(rawBody, "base64") : rawBody;

  console.log(`Invoking ${method} on ${url.toString()}`);

  return axios
    .request({
      method: method.toLowerCase(),
      url: url.toString(),
      headers: rawHeaders,
      data: decodedBody,
      timeout: deadline,
    })
    .then((response) => {
      const { data: rawData, headers: rawHeaders } = response;

      const body =
        rawData && typeof rawData === "string"
          ? rawData
          : Buffer.from(rawData).toString("base64");

      const isBase64Encoded = rawData && typeof rawData !== "string";

      const payload: APIGatewayProxyResultV2 = {
        statusCode: response.status,
        headers: convertHeaders(rawHeaders),
        body,
        isBase64Encoded,
      };

      return {
        requestId,
        payload,
      };
    });
};

// export const endpointProxy = async (endpoint: URL): Promise<void> => {
//   return axios
//     .get(
//       `http://${AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime/invocation/next`,
//       { timeout: 0 }
//     )
//     .then(({ headers, data }) => {
//       const requestId = headers["Lambda-Runtime-Aws-Request-Id"] as string;
//       const deadline = Number.parseInt(headers["Lambda-Runtime-Deadline-Ms"]);

//       console.log("Received request from Lambda Runtime API", { requestId });

//       let event = data as APIGatewayProxyEventV2;
//       const {
//         requestContext,
//         rawPath,
//         rawQueryString,
//         headers: rawHeaders,
//         body: rawBody,
//         isBase64Encoded,
//       } = event;
//       const method = requestContext.http.method;

//       const url = new URL(rawPath, endpoint);
//       if (rawQueryString) {
//         url.search = new URLSearchParams(rawQueryString).toString();
//       }

//       const decodedBody =
//         isBase64Encoded && rawBody ? Buffer.from(rawBody, "base64") : rawBody;

//       const request: axios.AxiosRequestConfig<any> = {
//         method: method.toLowerCase(),
//         url: url.toString(),
//         headers: rawHeaders,
//         data: decodedBody,
//         timeout: deadline,
//       };

//       return axios
//         .request(request)
//         .then((response) => ({ requestId, response }));
//     })
//     .then(({ requestId, response }) => {
//       const { data: rawData, headers: rawHeaders } = response;

//       const body =
//         rawData && typeof rawData === "string"
//           ? rawData
//           : Buffer.from(rawData).toString("base64");

//       const isBase64Encoded = rawData && typeof rawData !== "string";

//       const payload: APIGatewayProxyResultV2 = {
//         statusCode: response.status,
//         headers: convertHeaders(rawHeaders),
//         body,
//         isBase64Encoded,
//       };

//       return { requestId, payload };
//     })
//     .then(({ requestId, payload }) => {
//       return axios.post(
//         `http://${AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime/invocation/${requestId}/response`,
//         payload
//       );
//     })
//     .then(({ config }) => {
//       console.log(`Invocation response successfully sent to ${config.url}`);
//     });
//   // TODO Error catcher?
// };

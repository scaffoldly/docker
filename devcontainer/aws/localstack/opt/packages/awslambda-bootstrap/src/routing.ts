import { APIGatewayProxyEventV2 } from "aws-lambda";
import axios from "axios";
import { EndpointRequest } from "./types";
import { endpointProxy } from "./proxy";

export const routeEvents = async (
  runtimeApi: string,
  endpoint: string
): Promise<void> => {
  const { headers, data } = await axios.get(
    `http://${runtimeApi}/2018-06-01/runtime/invocation/next`,
    {
      // block indefinitely until a response is received
      timeout: 0,
    }
  );

  const requestId = headers["Lambda-Runtime-Aws-Request-Id"] as string;

  console.log("Received request from Lambda Runtime API", { requestId });

  const initialDeadline = Number.parseInt(
    headers["Lambda-Runtime-Deadline-Ms"]
  );

  const event = JSON.parse(data) as APIGatewayProxyEventV2;

  const request: EndpointRequest = {
    requestId,
    endpoint,
    event,
    initialDeadline,
  };

  const { payload } = await endpointProxy(request);

  await axios.post(
    `http://${runtimeApi}/2018-06-01/runtime/invocation/${requestId}/response`,
    payload
  );

  console.log("Invocation response successfully sent to Lambda Runtime API", {
    requestId,
  });

  return routeEvents(runtimeApi, endpoint);
};

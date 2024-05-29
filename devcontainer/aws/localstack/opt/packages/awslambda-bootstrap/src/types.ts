import { APIGatewayProxyEventV2, APIGatewayProxyResultV2 } from "aws-lambda";

export type EndpointRequest = {
  requestId: string;
  endpoint: string;
  event: APIGatewayProxyEventV2;
  initialDeadline: number;
};

export type EndpointResponse = {
  requestId: string;
  payload: APIGatewayProxyResultV2;
};

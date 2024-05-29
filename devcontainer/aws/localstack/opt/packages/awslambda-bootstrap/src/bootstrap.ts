import { ChildProcess, spawn } from "child_process";
import which from "which";
import { routeEvents } from "./routing";
const { _HANDLER, IS_OFFLINE, AWS_LAMBDA_RUNTIME_API } = process.env;

export const bootstrap = async (): Promise<void> => {
  if (!AWS_LAMBDA_RUNTIME_API) {
    throw new Error("No AWS_LAMBDA_RUNTIME_API specified");
  }

  if (!_HANDLER) {
    throw new Error("No handler specified");
  }

  const handler = new URL(_HANDLER);

  let app: string = handler.protocol.slice(0, -1);
  let endpoint = handler.toString();
  let childProcess: ChildProcess | undefined = undefined;

  if (app !== "http" && app !== "https") {
    endpoint = handler.pathname;
    try {
      await which(app);
    } catch (error) {
      throw new Error(
        `Could not find \`${app}\` in system path ${process.env.PATH}`
      );
    }

    const subcommand = IS_OFFLINE === "true" ? "dev" : "start";

    childProcess = spawn(app, [subcommand], {
      detached: true,
      stdio: "inherit",
    });
  }

  try {
    await routeEvents(AWS_LAMBDA_RUNTIME_API, endpoint);
  } catch (e) {
    if (childProcess) {
      childProcess.kill();
    }
    throw e;
  }
};

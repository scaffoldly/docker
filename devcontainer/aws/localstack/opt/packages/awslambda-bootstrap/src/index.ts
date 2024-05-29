import packageJson from "../package.json";
import { bootstrap } from "./bootstrap";

(async () => {
  if (process.argv.includes("--version")) {
    console.log(packageJson.version);
    return;
  }

  try {
    await bootstrap();
  } catch (e) {
    if (e instanceof Error) {
      console.error(e.message);
    } else {
      console.error(e);
    }
    process.exit(1);
  }
})();

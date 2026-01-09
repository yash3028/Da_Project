import app from "./index";
import { connect_to_database } from "./config/database";

(async () => {
  await connect_to_database();
  app.listen(3002, () => console.log("Server running on 3002"));
})();

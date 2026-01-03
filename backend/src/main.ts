import app from "./index";
import { connect_to_database } from "./config/database";

(async () => {
  await connect_to_database();
  app.listen(3001, () => console.log("Server running on 3001"));
})();

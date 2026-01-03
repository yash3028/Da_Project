import "reflect-metadata";
import express from "express";
import cors from "cors";
import { Application, NextFunction, Request, Response } from "express";
import user_router from "./controller/userController";

const app = express();
app.use(cors());
app.use(express.json());

app.use("/api/auth", user_router);

app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  console.log(error.message);
  if (error instanceof Error) {
    res.status(400).json({ message: error.message });
  }
  res.status(500).json("Error");
});
export default app;

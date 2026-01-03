import { Request, Response, NextFunction, Router } from "express";
import { login, signup } from "../services/userServices";
const axios = require("axios");

const router: Router = Router();
router.post(
  "/save-user",
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const result = await signup(req.body);
      return res.status(201).json({
        message: "User created successfully",
      });
    } catch (error: any) {
      console.error("Signup error:", error);

      return res.status(400).json({
        message: error.message || "Signup failed",
      });
    }
  }
);

router.post(
  "/login",
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const login_response = await login(req.body);
      if (login_response?.success) {
        res
          .status(200)
          .json({ message: "successful", token: login_response.token });
      } else {
        res.status(401).json({ message: "unauthorized" });
      }
    } catch (error) {
      next(error);
    }
  }
);

router.post("/budget", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:5001/predict/budget",
      req.body
    );

    res.json(response.data);
  } catch (error) {
    console.error("error");
    res.status(500).json({ error: "ML service error" });
  }
});

router.post("/duration", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:5001/predict/duration",
      req.body
    );

    res.json(response.data);
  } catch (error) {
    console.error("Duration ML error:");
    res.status(500).json({ error: "ML duration service error" });
  }
});

export = router;

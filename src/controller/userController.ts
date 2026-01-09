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

router.post(
  "/borrow",
  async (req: Request, res: Response, next: NextFunction) => {}
);

export = router;

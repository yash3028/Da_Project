import { data_source } from "../config/database";
import { users } from "../entity/user";
import { Credentials } from "../model/cred";
import { generateJWT, payload } from "../utils/jwtUtils";

export async function signup(user: users) {
  try {
    const repo = data_source.getRepository(users);
    return await repo.save(user);
  } catch (error) {
    throw new Error("new");
  }
}

export const login = async (cred: Credentials) => {
  try {
    const repo = data_source.getRepository(users);
    const response = await repo.findOne({
      where: {
        username: cred.username,
      },
    });
    if (response?.password === cred.password) {
      const userPayload = payload(response.username);
      const token = generateJWT(userPayload);

      response.token = token;
      await repo.save(response);
      return { success: true, token };
    } else {
      return { success: false };
    }
  } catch (error) {
    throw error;
  }
};

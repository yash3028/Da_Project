import jwt from "jsonwebtoken";
import { TokenPayload } from "../model/tokenpayload";

/*export function generateKey():string{
    return crypto.randomBytes(64).toString('hex')
}*/

const key = "jbjasdbsjdbsj";

export function payload(username: string) {
  return { username };
}

export function generateJWT(payload: object): string {
  return jwt.sign(payload, key, { expiresIn: "1h" });
}

export async function verification(
  token: string
): Promise<null | TokenPayload> {
  try {
    let payload: TokenPayload | null = null;
    jwt.verify(token, key, { complete: true }, function (error, decoded) {
      if (error) {
        throw error;
      } else {
        payload = decoded?.payload as TokenPayload;
      }
    });
    return payload;
  } catch (error) {
    throw error;
  }
}

export type Role =
  | "umkm"
  | "pendamping"
  | "mentor"
  | "admin_b2g"
  | "admin_platform";

export type UserStatus = "active" | "invited" | "suspended" | "deleted";

export type User = {
  id: string;
  tenant_id: string;
  email: string;
  full_name: string;
  phone: string | null;
  role: Role;
  status: UserStatus;
  last_login_at: string | null;
};

export type AuthResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
};

export type Problem = {
  type?: string;
  title: string;
  status: number;
  detail?: string;
  code: string;
  trace_id?: string;
  errors?: { field: string; message: string }[];
};

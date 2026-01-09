import { Role } from '../../../@core/auth/models/role.enum';


export interface User {
  _id: string;
  account_id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: Role;
  disabled: boolean;
  verified: boolean;
  created_at: Date;
  updated_at: Date;
}

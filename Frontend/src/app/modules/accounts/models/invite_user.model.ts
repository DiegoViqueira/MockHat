import { Role } from "../../../@core/auth/models/role.enum"



export interface InviteUserToAccount {
    email: string;
    role: Role;
}

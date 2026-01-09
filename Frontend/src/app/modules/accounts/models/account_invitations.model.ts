import { Role } from "../../../@core/auth/models/role.enum"

export interface AccountInvitation {
    id: string;
    account_id: string;
    email: string;
    role: Role;
    created_at: Date;
    updated_at: Date;
}



export interface ListInvitations {
    invitations: AccountInvitation[];
    total: number;
}



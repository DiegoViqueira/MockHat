import { User } from '../../users/models/user.model';
import { UserPlan } from '../../users/models/plan.enum';

export interface Account {
    id: string;
    name: string;
    plan: UserPlan;
    owner: User;
    users: User[];
    created_at: Date;
    updated_at: Date;
    is_active: boolean;
    stripe_customer_id: string;
}



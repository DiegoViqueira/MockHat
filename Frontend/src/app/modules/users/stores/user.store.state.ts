import { User } from '../models/user.model';


export type UserStoreQueryParams = {
  query: string;
  limit: number;
  offset: number;
};

type UserStoreState = {
  user: User;
  users: User[];
  total: number;
  isLoading: boolean;
  query: UserStoreQueryParams;
};

export const UserStoreInitialState: UserStoreState = {
  user: undefined,
  users: [],
  total: 0,
  isLoading: false,
  query: { query: '', limit: 1000, offset: 0 },
};

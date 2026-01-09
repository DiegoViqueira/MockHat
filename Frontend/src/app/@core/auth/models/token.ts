/*
 * Copyright (c) Herta 2023. All Rights Reserved.
 *
 */

export interface Token {
  Access: string;
  Refresh: string;
}

export interface GoogleTokenRequest {
  token: string;
}

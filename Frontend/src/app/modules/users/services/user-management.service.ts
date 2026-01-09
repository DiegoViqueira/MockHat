import { Injectable, signal, WritableSignal } from '@angular/core';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { HttpService } from '../../../@core/services/http.service';
import { User } from '../models/user.model';
import { ListUsers } from '../models/list.users.model';

@Injectable({
  providedIn: 'root',
})
export class UserManagementService {

  constructor(private readonly api: HttpService) { }


  search(limit, offset): Observable<ListUsers> {
    return this.api.get(`users?limit=${limit}&offset=${offset}`).pipe(
      map((response) => {
        return response;
      }),

    );
  }

  actives(): Observable<ListUsers> {
    return this.api.get(`users/active/all`).pipe(
      map((response) => {
        return response;
      })
    );
  }

  register(user: User): Observable<User> {
    return this.api
      .post(`users`, user).pipe(
        map((response) => {
          return response;
        })
      );
  }

  update(user: User): Observable<User> {
    return this.api
      .patch(`users`, user._id, user).pipe(
        map((response) => {
          return response;
        })
      );
  }


  me(): Observable<User> {
    return this.api.get(`users/active/me`).pipe(
      map((result) => {
        return result;
      })
    );
  }
  changePassword(request: {
    Username: string;
    Password: string;
    NewPassword: string;
  }): Observable<void> {
    return this.api.post(`ChangePassword`, request).pipe(
      map((response) => {
        return response;
      })
    );
  }
}

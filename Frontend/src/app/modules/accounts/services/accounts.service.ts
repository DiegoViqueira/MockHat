import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { Account } from '../models/account.model';
import { InviteUserToAccount } from '../models/invite_user.model';
import { ListInvitations } from '../models/account_invitations.model';


@Injectable({
    providedIn: 'root'
})
export class AccountsService {
    private apiUrl = `${environment.apiUrl}/accounts`;

    constructor(private http: HttpClient) { }


    getAccount(): Observable<Account> {
        return this.http.get<Account>(`${this.apiUrl}`);
    }

    inviteUser(data: InviteUserToAccount): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/invite-user`, data);
    }

    getInvitations(): Observable<ListInvitations> {
        return this.http.get<ListInvitations>(`${this.apiUrl}/invitations`);
    }



} 
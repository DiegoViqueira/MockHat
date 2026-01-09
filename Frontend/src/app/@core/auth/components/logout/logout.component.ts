import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
    selector: 'app-logout',
    templateUrl: './logout.component.html',
    standalone: false
})
export class LogoutComponent {

    constructor(private authService: AuthService) {
        this.authService.logout().subscribe();
    }


}

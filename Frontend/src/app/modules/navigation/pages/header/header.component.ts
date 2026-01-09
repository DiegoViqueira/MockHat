import { Component, computed, inject, Input, Signal } from '@angular/core';
import { AuthService } from '../../../../@core/auth/services/auth.service';
import { User } from '../../../../@core/auth/models/users';
import { SessionService } from '../../../../@core/auth/services/session.service';
import { Router } from '@angular/router';
import { finalize } from 'rxjs/operators';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { UserStore } from '../../../users/stores/user.store';
import { MatSidenav } from '@angular/material/sidenav';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';
import { canMatchAdminRoleGuard } from '../../../../@core/auth/guards/canMatchRoleGuard';
@Component({
  selector: 'hrt-header',
  styleUrls: ['./header.component.scss'],
  templateUrl: './header.component.html',
  standalone: false
})
export class HeaderComponent {
  user: Signal<User | null>;

  private readonly deviceDetectionService = inject(DeviceDetectionService);
  protected readonly isMobile = computed(() => this.deviceDetectionService.isMobileScreen());

  @Input() snav: MatSidenav;

  user_store = inject(UserStore);

  constructor(
    private readonly authService: AuthService,
    private readonly router: Router,
    session: SessionService
  ) {
    this.user = session.user;
    this.user_store.active();
  }

  logOut() {
    this.authService
      .logout()
      .pipe(finalize(() => this.router.navigateByUrl('auth/login')))
      .subscribe();
  }
  isAdmin = canMatchAdminRoleGuard();

  account() {
    this.router.navigate([AppRoutes.Modules, AppRoutes.Account]);
  }

  students() {
    this.router.navigate([AppRoutes.Modules, AppRoutes.Students]);
  }


}

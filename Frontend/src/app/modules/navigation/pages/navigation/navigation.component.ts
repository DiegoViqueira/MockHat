import { Component, computed, effect, inject } from '@angular/core';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { RoutesByRole } from '../../../../@core/auth/models/routes-by-role';
import { NavigationEnd, Router } from '@angular/router';
import { NavigationItem } from '../../models/navigation.item';
import { SessionService } from '../../../../@core/auth/services/session.service';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';
import { AuthService } from '../../../../@core/auth/services/auth.service';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'wlk-navigation',
  templateUrl: './navigation.component.html',
  styleUrl: './navigation.component.scss',
  standalone: false
})
export class NavigationComponent {

  private readonly deviceDetectionService = inject(DeviceDetectionService);
  protected readonly isMobile = computed(() => this.deviceDetectionService.isMobileScreen());

  private readonly authService = inject(AuthService);

  navItems: NavigationItem[] = [];
  constructor(
    protected session: SessionService,
    private router: Router
  ) {

    effect(
      () => {
        if (this.session.user()) {
          this.filterMenuByUser();
          this.init();
        }
      },
      { allowSignalWrites: true }
    );
  }

  init() {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        if (event.url.includes('auth/logout')) {
          this.authService.logout().pipe(finalize(() => this.router.navigateByUrl('auth/login'))).subscribe();
        }
      }
    });
  }

  filterMenuByUser() {
    const routesByUSer = RoutesByRole.find((x) => x.role === this.session.user().role);
    if (routesByUSer === undefined) return;


    this.navItems = this.getItems().filter((ni) =>
      routesByUSer.routes.includes(ni.RoutingPath.split('/').pop() as AppRoutes) || ni.RoutingPath === AppRoutes.Logout
    );
  }

  getItems() {
    return [

      {
        Icon: 'home',
        Name: 'menu.home',
        RoutingPath: AppRoutes.Home,
      },
      {
        Icon: 'class',
        Name: 'menu.classes',
        RoutingPath: AppRoutes.Classes,
      },

      {
        Icon: 'group',
        Name: 'menu.students',
        RoutingPath: AppRoutes.Students,
      },
      // {
      //   Icon: 'draw',
      //   Name: 'menu.assessments',
      //   RoutingPath: AppRoutes.Assessments,
      // },
      // {
      //   Icon: 'settings',
      //   Name: 'menu.settings',
      //   RoutingPath: AppRoutes.Settings,
      // },
      // {
      //   Icon: 'payments',
      //   Name: 'menu.billing',
      //   RoutingPath: AppRoutes.Billing,
      // },
      {
        Icon: 'logout',
        Name: 'menu.logout',
        RoutingPath: AppRoutes.Logout,
      },
    ];
  }
}

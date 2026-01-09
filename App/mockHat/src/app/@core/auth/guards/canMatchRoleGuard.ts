import { CanMatchFn, Route } from '@angular/router';
import { inject } from '@angular/core';
import { RoutesByRole } from '../models/routes-by-role';
import { AppRoutes } from '../models/routes.enum';
import { SessionService } from '../services/session.service';

export const canMatchRoleGuard: CanMatchFn = (route: Route) => {
  const session = inject(SessionService);
  if (!session.user()) return false;
  const roleRoutes = RoutesByRole.find((x) => x.role === session.user()?.role);
  return roleRoutes?.routes.includes(route.path as AppRoutes) ?? false;
};

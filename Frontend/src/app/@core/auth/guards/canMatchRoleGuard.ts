import { CanMatchFn, Route } from '@angular/router';
import { inject } from '@angular/core';
import { RoutesByRole } from '../models/routes-by-role';
import { AppRoutes } from '../models/routes.enum';
import { SessionService } from '../services/session.service';
import { Role } from '../models/role.enum';

export const canMatchRoleGuard: CanMatchFn = (route: Route) => {
  const session = inject(SessionService);
  if (!session.user()) return false;
  return RoutesByRole.find((x) => x.role === session.user().role).routes.includes(
    route.path as AppRoutes
  );
};


export const canMatchAdminRoleGuard = () => {
  const session = inject(SessionService);
  if (!session.user()) return false;
  return session.user().role === Role.ADMIN || session.user().role === Role.OWNER;
};


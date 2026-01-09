import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { SessionService } from '../services/session.service';

export const canActivateAuthGuard: CanActivateFn = () => {
  const session = inject(SessionService);
  const router = inject(Router);
  if (!session.isExpired() || session.refreshToken()) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};

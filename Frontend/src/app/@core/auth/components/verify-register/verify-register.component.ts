import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'wlk-verify-register',
    templateUrl: './verify-register.component.html',
    styleUrl: './verify-register.component.scss',
    standalone: false
})
export class VerifyRegisterComponent {

  private readonly authService: AuthService = inject(AuthService);
  private readonly router: Router = inject(Router);
  private readonly route: ActivatedRoute = inject(ActivatedRoute);
  private readonly snackBar: MatSnackBar = inject(MatSnackBar);
  constructor() {
    this.route.queryParams.subscribe((params) => {
      this.authService.verifyRegister(params['token']).subscribe({
        next: () => {
          this.snackBar.open('Register verified', 'Close', { duration: 3000, panelClass: ['success-snackbar'] });
          this.router.navigate(['/auth/login']);
        },
        error: () => {
          this.snackBar.open('Error verifying register', 'Close', { duration: 3000, panelClass: ['error-snackbar'] });
        }
      });
    });
  }
}

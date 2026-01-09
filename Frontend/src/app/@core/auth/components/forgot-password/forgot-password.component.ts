import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
@Component({
    selector: 'wlk-forgot-password',
    templateUrl: './forgot-password.component.html',
    styleUrl: './forgot-password.component.scss',
    standalone: false
})
export class ForgotPasswordComponent {

  private authService = inject(AuthService);

  isLoading = false;
  constructor(private formBuilder: FormBuilder, private router: Router) { }

  form: FormGroup = this.formBuilder.group({
    email: ['', [Validators.required, Validators.email]],
  });

  onSubmit() {
    this.isLoading = true;
    this.authService.forgotPassword(this.form.value.email).subscribe({
      next: () => {
        this.isLoading = false;
        this.router.navigate(['/auth/mail-sent']);
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        console.log(error);
      }
    });
  }

}

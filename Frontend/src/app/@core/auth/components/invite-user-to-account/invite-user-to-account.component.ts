import { Component, inject } from '@angular/core';
import { LegalDocumentsComponent } from '../legal-documents/legal-documents.component';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder } from '@angular/forms';
import { FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { passwordPattern } from '../../../../@shared/common-environment/common-environment';
import { JwtHelperService } from '@auth0/angular-jwt';

@Component({
  selector: 'wlk-invite-user-to-account',
  templateUrl: './invite-user-to-account.component.html',
  styleUrl: './invite-user-to-account.component.scss',
  standalone: false
})
export class InviteUserToAccountComponent {
  form: FormGroup;
  hidePassword = true;
  isLoading = false;
  showEmailAlert = false;
  private authService = inject(AuthService);
  private router = inject(Router);
  private dialog = inject(MatDialog);
  private jwtHelper = inject(JwtHelperService);
  private route = inject(ActivatedRoute);


  data: any;
  constructor(
    private fb: FormBuilder,
    private snackBar: MatSnackBar
  ) {


    this.route.queryParams.subscribe((params) => {

      this.data = this.toData(params['token']);
      console.log(this.data);
      this.form = this.fb.group({
        account_name: [this.data.account_name, Validators.required],
        email: [this.data.email, [Validators.required, Validators.email]],
        first_name: ['', Validators.required],
        last_name: ['', Validators.required],
        password: ['', [Validators.required, Validators.pattern(passwordPattern)]],
        confirmPassword: ['', Validators.required],
        termsAndConditions: [false, Validators.requiredTrue],
        token: [params['token'], Validators.required]
      }, {
        validators: this.passwordMatchValidator
      });
    });
  }



  private passwordMatchValidator(form: FormGroup) {
    const password = form.get('password');
    const confirmPassword = form.get('confirmPassword');

    if (password?.value !== confirmPassword?.value) {
      confirmPassword?.setErrors({ passwordMismatch: true });
    } else {
      confirmPassword?.setErrors(null);
    }
    return null;
  }

  private toData(token: string): any {
    const decodeToken = this.jwtHelper.decodeToken(token);
    return {
      account_name: decodeToken.account_name ?? '',
      account_id: decodeToken.account_id ?? '',
      email: decodeToken.email ?? '',
      role: decodeToken.role ?? '',
    };
  }

  onSubmit(): void {
    if (this.form.valid) {
      this.isLoading = true;
      const formValue = this.form.value;

      this.authService.register(formValue).subscribe({
        next: () => {
          this.isLoading = false;
          this.router.navigate(['/auth/mail-sent']);
        },
        error: (error: HttpErrorResponse) => {
          this.isLoading = false;
          if (error.status === 400) {
            this.snackBar.open(error.error.detail, 'Cerrar', {
              duration: 5000,
              panelClass: ['error-snackbar']
            });
          } else {
            this.snackBar.open('Error en el registro', 'Cerrar', {
              duration: 5000,
              panelClass: ['error-snackbar']
            });
          }
        }
      });
    }
  }

  legalDocument(type: string) {
    this.dialog.open(LegalDocumentsComponent, {
      width: '90%',
      maxWidth: '90%',
      data: { type: type },
    });
  }

}

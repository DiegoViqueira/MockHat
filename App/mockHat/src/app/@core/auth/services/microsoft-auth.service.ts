import { inject, Injectable } from '@angular/core';

import * as msal from '@azure/msal-browser';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';
import { SessionService } from './session.service';

@Injectable({
  providedIn: 'root',
})
export class MicrosoftAuthService {
  private msalInstance: msal.PublicClientApplication;
  private authService = inject(AuthService);
  private session = inject(SessionService);

  constructor(private readonly router: Router) {
    const currentUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}${this.router.url}`;

    this.msalInstance = new msal.PublicClientApplication({
      auth: {
        clientId: '********************************',
        authority: 'https://login.microsoftonline.com/common',
        redirectUri: currentUrl,
      },
    });
  }

  async init() {


    await this.msalInstance.initialize().catch((error) => {
      console.error('Error al inicializar MSAL:', error);
    });

    await this.handleRedirectCallback();
    this.session.onClose.subscribe(() => this.close());
  }

  async loginWithMicrosoft(): Promise<void> {
    console.info('Login WIth Micrisoft');
    try {
      if (!this.msalInstance) {
        console.warn('MSAL aún no se ha inicializado.');
        return;
      }

      await this.msalInstance.loginRedirect({
        scopes: ['openid', 'profile', 'email'],
        state: 'microsoft',
      });
    } catch (error) {
      console.error('Error durante el inicio de sesión:', error);
    }
  }

  async handleRedirectCallback(): Promise<void> {

    this.msalInstance
      .handleRedirectPromise()
      .then((response) => {
        const state = response?.state;
        if (response && state === 'microsoft' && response.idToken) {
          this.authService
            .loginWithMicrosoft(response.idToken)
            .subscribe(() => this.router.navigateByUrl('/modules'));
        }
      })
      .catch((error) => {
        console.error('Error al manejar la redirección:', error);
      });
  }

  private close() {
    if (this.msalInstance.getAllAccounts().length === 0) {
      return;
    }
    const currentUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/login`;

    this.msalInstance.logoutRedirect({
      account: this.msalInstance.getActiveAccount(),
      postLogoutRedirectUri: currentUrl,
    });
  }
}

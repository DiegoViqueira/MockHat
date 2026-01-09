import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../@core/auth/services/auth.service';
import { Router } from '@angular/router';
import { MicrosoftAuthService } from '../@core/auth/services/microsoft-auth.service';
import { api_google } from 'src/environments/environment';
import { Capacitor } from '@capacitor/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {


  hide = true;
  year = new Date().getFullYear();

  constructor(private readonly service: AuthService,
    private readonly router: Router,
    private microsoftService: MicrosoftAuthService) {

  }
  async ngOnInit() {
    const params = new URLSearchParams(window.location.hash.substring(1)); // Elimina el símbolo '#'
    const accessToken = params.get('id_token');

    if (accessToken) {
      this.handleCredentialResponse(accessToken);
    } else {
      //this.clearUrlHash();
    }
    await this.microsoftService.init();


  }

  handleCredentialResponse(token: any) {
    const params = new URLSearchParams(window.location.hash.substring(1)); // Remove '#'
    const idToken = params.get('id_token');
    const state = params.get('state');

    if (state === 'google' && idToken) {
      this.service.loginWithGoogle(idToken).subscribe(() => this.router.navigateByUrl('/modules'));
    } else {
      console.warn('Unhandled state or invalid Google response:', state);
    }
  }


  togglePasswordVisibility() {
    this.hide = !this.hide;
  }

  clearUrlHash(): void {
    history.replaceState(null, '', window.location.pathname);
  }

  loginWithGoogle(): void {

    const redirectUri = Capacitor.isNativePlatform()
      ? 'com.mockhat:/login' // URL para aplicaciones móviles
      : `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}${this.router.url}`; // URL para aplicaciones web

    const googleAuthUrl = new URL('https://accounts.google.com/o/oauth2/auth');
    googleAuthUrl.searchParams.set('client_id', api_google.id);
    googleAuthUrl.searchParams.set('redirect_uri', redirectUri.toString());
    googleAuthUrl.searchParams.set('response_type', 'id_token');
    googleAuthUrl.searchParams.set('scope', 'openid email profile');
    googleAuthUrl.searchParams.set('state', 'google');
    window.location.href = googleAuthUrl.toString();
  }

  loginWithMicrosoft() {
    this.microsoftService.loginWithMicrosoft();

  }

  onLegal() {
    console.log('Legal terms clicked');
  }

  goToMockHat() {
    console.log('Navigating to MockHat');
  }
}

import { Component, inject } from '@angular/core';
import { stripe_pk } from '../../../../../environments/environment';
import { UserStore } from '../../../users/stores/user.store';
import { CustomerService } from '../../services/customer.service';
import { Router } from '@angular/router';

@Component({
    selector: 'wlk-plan-info',
    templateUrl: './plan-info.component.html',
    styleUrl: './plan-info.component.scss',
    standalone: false
})
export class PlanInfoComponent {
  user_store = inject(UserStore);
  service = inject(CustomerService);

  protected readonly stripe_pk = stripe_pk;
  plans: any = undefined;
  current_subscription: any = undefined;

  constructor(private router: Router) {
    this.service.currentSubscription().subscribe((x) => {
      this.current_subscription = x;
    });
    this.service.getPrices().subscribe((x) => {
      this.plans = x.filter((x) => x.interval === 'month').sort((a, b) => a.amount - b.amount);
    });
  }

  redirectToCustomerPortal() {
    try {
      const currentUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}${this.router.url}`;

      this.service.getPortal(currentUrl).subscribe((x) => {
        window.location.href = x.portal_url;
      });
    } catch (error) {
      console.error('Error creating portal session:', error);
    }
  }

  subscribeToPlan(id) {
    const currentUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}${this.router.url}`;

    console.info(id);
    this.service.suscribe({ price_id: id, fallback_url: currentUrl }).subscribe((x) => {
      window.location.href = x.checkout_url;
    });
  }
}

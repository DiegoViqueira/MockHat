import { Component, computed, effect, inject, OnInit, signal } from '@angular/core';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { AccountsService } from '../../services/accounts.service';
import { Account } from '../../models/account.model';
import { MatDialog } from '@angular/material/dialog';
import { InviteUserComponent } from '../../components/invite-user/invite-user.component';
import { ListInvitations } from '../../models/account_invitations.model';
import { UserPlan } from '../../../users/models/plan.enum';
import { PlanGroup, plans } from '../../../../@shared/common-environment/common-environment';
@Component({
  selector: 'wlk-account',
  templateUrl: './account.component.html',
  styleUrl: './account.component.scss',
  standalone: false
})
export class AccountComponent implements OnInit {

  backUrl: any = {
    route: [AppRoutes.Modules, AppRoutes.Classes],
  };

  account = signal<Account | null>(null);
  invitations = signal<ListInvitations | null>(null);
  displayedColumns: string[] = ['email', 'role'];
  plans_business = plans[PlanGroup.BUSINESS].plans;
  plans_individual = plans[PlanGroup.INDIVIDUAL].plans;
  selectedPlan = signal<string | null>(null);
  inviteUserDialog = inject(MatDialog);
  isBussines = computed(() => this.account()?.plan === UserPlan.BUSINESS || this.account()?.plan === UserPlan.BUSINESS_PRO);


  getSelectedTabIndex(): number {
    if (!this.isBussines()) {
      return 0; // índice del tab BUSINESS
    } else if (this.isBussines()) {
      return 1; // índice del tab INDIVIDUAL
    }
    return 0; // por defecto muestra el primer tab
  }

  upgradePlan(plan: string) {
    console.log(plan);
  }

  constructor(private accountsService: AccountsService) {
    effect(() => {
      this.selectedPlan.set(this.account()?.plan);
    });
  }

  ngOnInit(): void {
    this.initAccount();
  }

  initAccount() {
    this.accountsService.getAccount().subscribe((account) => {
      this.account.set(account);
      this.accountsService.getInvitations().subscribe((invitations) => {
        this.invitations.set(invitations);
      });
    });
  }

  openInviteUserDialog() {
    this.inviteUserDialog.open(InviteUserComponent, {
      width: '50%',
      height: '50%'
    }).afterClosed().subscribe((data) => {
      if (data) {
        this.accountsService.inviteUser(data).subscribe((response) => {
          this.initAccount();
        });
      }
    });
  }

}

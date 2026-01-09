import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InviteUserToAccountComponent } from './invite-user-to-account.component';

describe('InviteUserToAccountComponent', () => {
  let component: InviteUserToAccountComponent;
  let fixture: ComponentFixture<InviteUserToAccountComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InviteUserToAccountComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InviteUserToAccountComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

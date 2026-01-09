import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddMemberToClassComponent } from './add-member-to-class.component';

describe('AddMemberToClassComponent', () => {
  let component: AddMemberToClassComponent;
  let fixture: ComponentFixture<AddMemberToClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddMemberToClassComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddMemberToClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

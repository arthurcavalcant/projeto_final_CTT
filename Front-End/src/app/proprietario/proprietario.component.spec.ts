import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProprietarioComponent } from './proprietario.component';

describe('ProprietarioComponent', () => {
  let component: ProprietarioComponent;
  let fixture: ComponentFixture<ProprietarioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProprietarioComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProprietarioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

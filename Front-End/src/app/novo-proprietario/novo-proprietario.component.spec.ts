import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NovoProprietarioComponent } from './novo-proprietario.component';

describe('NovoProprietarioComponent', () => {
  let component: NovoProprietarioComponent;
  let fixture: ComponentFixture<NovoProprietarioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NovoProprietarioComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NovoProprietarioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

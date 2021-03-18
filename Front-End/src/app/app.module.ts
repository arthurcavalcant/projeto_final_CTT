import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from '@angular/common/http';


import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {ClienteComponent} from './cliente/cliente.component';
import {ClientesComponent} from './clientes/clientes.component';
import { NovoClienteComponent } from './novo-cliente/novo-cliente.component';
import { ProprietarioComponent } from './proprietario/proprietario.component';
import { ProprietariosComponent } from './proprietarios/proprietarios.component';
import { NovoProprietarioComponent } from './novo-proprietario/novo-proprietario.component';
import { NovoImovelComponent } from './novo-imovel/novo-imovel.component';
import { ImoveisComponent } from './imoveis/imoveis.component';
import { ImovelComponent } from './imovel/imovel.component';
import { VendedorComponent } from './vendedor/vendedor.component';
import { VendedoresComponent } from './vendedores/vendedores.component';
import { NovoVendedorComponent } from './novo-vendedor/novo-vendedor.component';
import { VendasComponent } from './vendas/vendas.component';
import { NovaVendaComponent } from './nova-venda/nova-venda.component';

@NgModule({
  declarations: [
    AppComponent,
    ClienteComponent,
    ClientesComponent,
    NovoClienteComponent,
    ProprietarioComponent,
    ProprietariosComponent,
    NovoProprietarioComponent,
    NovoImovelComponent,
    ImoveisComponent,
    ImovelComponent,
    VendedorComponent,
    VendedoresComponent,
    NovoVendedorComponent,
    VendasComponent,
    NovaVendaComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}

import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ClientesComponent} from './clientes/clientes.component';
import {ClienteComponent} from "./cliente/cliente.component";
import {NovoClienteComponent} from "./novo-cliente/novo-cliente.component";
import {ProprietariosComponent} from "./proprietarios/proprietarios.component";
import {ProprietarioComponent} from "./proprietario/proprietario.component";
import {NovoProprietarioComponent} from "./novo-proprietario/novo-proprietario.component";
import {ImoveisComponent} from "./imoveis/imoveis.component";
import {ImovelComponent} from "./imovel/imovel.component";
import {NovoImovelComponent} from "./novo-imovel/novo-imovel.component";
import {VendedorComponent} from "./vendedor/vendedor.component";
import {VendedoresComponent} from "./vendedores/vendedores.component";
import {NovoVendedorComponent} from "./novo-vendedor/novo-vendedor.component";
import {VendasComponent} from "./vendas/vendas.component";
import {NovaVendaComponent} from "./nova-venda/nova-venda.component";

const routes: Routes = [
  {path: 'clientes', component: ClientesComponent},
  {path: 'cliente', component: ClienteComponent},
  {path: 'novoCliente', component: NovoClienteComponent},
  {path: 'proprietarios', component: ProprietariosComponent},
  {path: 'proprietario', component: ProprietarioComponent},
  {path: 'novoProprietario', component: NovoProprietarioComponent},
  {path: 'imoveis', component: ImoveisComponent},
  {path: 'imovel', component: ImovelComponent},
  {path: 'novoImovel', component: NovoImovelComponent},
  {path: 'vendedor', component: VendedorComponent},
  {path: 'vendedores', component: VendedoresComponent},
  {path: 'novoVendedor', component: NovoVendedorComponent},
  {path: 'vendas', component: VendasComponent},
  {path: 'novaVenda', component: NovaVendaComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}

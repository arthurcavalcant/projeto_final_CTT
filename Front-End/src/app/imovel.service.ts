import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ImovelService {
  constructor(private httpClient: HttpClient) { }

  public getImoveis(){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns4/imovel/`);
  }
  public getImovel(idimovel:any){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns4/imovel/${idimovel}`);
  }
  public deleteImovel(idimovel:any){
    return this.httpClient.delete(`http://127.0.0.1:5000/api/ns4/imovel/${idimovel}`);
  }
  public putImovelCadastrado(idimovel:any, imovel:any){
    return this.httpClient.put(`http://127.0.0.1:5000/api/ns4/imovel/${idimovel}`, imovel);
  }
  public postImovel(imovel:any){
    return this.httpClient.post(`http://127.0.0.1:5000/api/ns4/imovel/`, imovel);
  }


}

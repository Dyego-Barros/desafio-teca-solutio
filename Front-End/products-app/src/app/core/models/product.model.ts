export interface Product {
  id?: number;
  nome: string;
  marca: string;
  valor: number;
  in_stock: boolean;
  created_at?: string;
  updated_at?: string;
}

function c=lpc_to_cep(a)
dim=length(a);
c=zeros(dim,1);
c(1)=a(1);
for k=2:dim
    c(k)=a(k);
    for n=1:k-1
        c(k)=c(k)+1/k*a(n)*(k-n)*c(k-n);
    end
end
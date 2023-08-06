from pycsp3 import *

pizzaPrices = data.pizzaPrices
vouchers = data.vouchers
nPizzas, nVouchers = len(pizzaPrices), len(vouchers)

# v[i] is the voucher used for the ith pizza. 0 means that no voucher is used.
#  A negative (resp., positive) value i means that the ith pizza contributes to the the pay (resp., free) part of voucher |i|.
v = VarArray(size=nPizzas, dom=range(-nVouchers, nVouchers + 1))

# np[i] is the number of paid pizzas wrt the ith voucher
np = VarArray(size=nVouchers, dom=lambda i: {0, vouchers[i].payPart})

# nf[i] is the number of free pizzas wrt the ith voucher
nf = VarArray(size=nVouchers, dom=lambda i: range(vouchers[i].freePart + 1))

# pp[i] is the price paid for the ith pizza
pp = VarArray(size=nPizzas, dom=lambda i: {0, pizzaPrices[i]})

satisfy(

    #  counting paid pizzas
    [Count(v, value=-i - 1) == np[i] for i in range(nVouchers)],

    #  counting free pizzas
    [Count(v, value=i + 1) == nf[i] for i in range(nVouchers)],

    #  a voucher, if used, must contribute to have at least one free pizza.
    [iff(nf[i] == 0, np[i] != vouchers[i].payPart) for i in range(nVouchers)],

    #  a pizza must be paid iff a free voucher part is not used to have it free
    [imply(v[i] <= 0, pp[i] != 0) for i in range(nPizzas)],

    #  a free pizza obtained with a voucher must be cheaper than any pizza paid wrt this voucher
    [(v[i] >= v[j]) | (v[i] != -v[j]) for i in range(nPizzas) for j in range(nPizzas) if i != j and pizzaPrices[i] < pizzaPrices[j]]
)


minimize(
    # minimizing summed up price paid for pizzas
    Sum(pp)
)

annotate(decision=v)


# coding: utf-8
import ipaddress

from urllib.parse import urlparse
from pydantic import BaseModel
from utils.env import Env


class BasicsPayload(BaseModel):
    url: str
    scheme: str
    host: str
    domain: str
    is_valid: bool


def get(url) -> BasicsPayload:
    if not url.startswith(("http://", "https://")):
        return BasicsPayload(**{
            "url": url,
            "scheme": "",
            "host": "",
            "domain": "",
            "is_valid": False,
        })
    ue = urlparse(url)
    host = clear(ue.hostname)
    if not is_valid(host):
        return BasicsPayload(**{
            "url": url,
            "scheme": "",
            "host": "",
            "domain": "",
            "is_valid": False,
        })
    return BasicsPayload(**{
        "url": url,
        "scheme": ue.scheme,
        "host": clear(ue.netloc),
        "domain": domain(host),
        "is_valid": True,
    })


def is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except:
        return False


def clear(url: str) -> str:
    for rep in Env.URL_REPLACE.split(" "):
        url = url.replace(rep, "")
    return url


def domain(host: str) -> str:
    if host.count(".") < 2:
        return host
    if is_ip(host):
        return host
    hosts = host.split(".")
    if hosts[-2] in domain_suffix and hosts[-1] in country_suffix:
        return ".".join(hosts[-3:-1])
    return ".".join(host.split(".")[-2:])


def is_valid(host: str) -> bool:
    return bool(host.count(".") > 0 and not (host.startswith(".") or host.endswith(".")))


domain_suffix = """
com
org
net
gov
edu
mil
int
info
biz
name
pro
coop
museum
aero
jobs
mobi
""".strip().split("\n")
domain_suffix = tuple(domain_suffix)
country_suffix = """
cn
tw
hk
mo
jp
kp
kr
mn
mm
bn
kh
tl
id
la
my
ph
sg
th
vn
bd
bt
in
mv
np
pk
lk
kz
kg
tj
tm
uz
af
az
bh
am
cy
ge
tr
ir
iq
il
jo
kw
lb
om
ps
qa
sa
sy
ae
ye
be
fr
ie
lu
mc
nl
uk
at
de
li
ch
dk
fi
is
no
se
ru
by
ee
lv
lt
md
ua
pl
sk
hu
cz
al
hr
gr
it
mk
mt
me
pt
ro
sm
rs
si
es
va
us
ca
mx
cu
jm
ht
bs
dm
do
bb
gd
lc
ag
kn
vc
tt
ar
br
cl
co
pe
ve
bo
ec
gy
py
sr
uy
bz
cr
sv
gt
hn
ni
pa
ai
aw
bm
ky
gl
an
pr
mf
gf
fk
vi
tc
dz
eg
ly
ma
tn
sd
ss
ng
gh
bj
bf
td
ci
gm
gn
gw
lr
ml
ne
mr
sn
sl
tg
cv
cm
gq
ga
cg
cd
cf
st
za
ao
bw
km
ls
mg
mw
mu
mz
na
sz
zm
zw
bi
dj
er
et
ke
rw
sc
so
tz
ug
au
nz
fj
pw
ws
to
tv
ki
mh
fm
nr
pg
sb
vu
cx
ck
pf
gu
nc
nu
pn
tk
""".strip().split("\n")
country_suffix = tuple(country_suffix)

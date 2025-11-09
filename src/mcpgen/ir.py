from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Meta:
    irVersion: str
    specDigest: str
    source: str
    generatedAt: str

@dataclass_json
@dataclass
class Service:
    id: str
    title: str
    version: str
    description: Optional[str] = None
    baseUrls: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class Server:
    url: str
    variables: Dict[str, Any] = field(default_factory=dict)

@dataclass_json
@dataclass
class OAuthFlow:
    type: str
    tokenUrl: Optional[str] = None
    authUrl: Optional[str] = None
    refreshUrl: Optional[str] = None
    scopes: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class SecurityScheme:
    id: str
    type: str
    name: str
    in_val: Optional[str] = None
    scheme: Optional[str] = None
    flows: List[OAuthFlow] = field(default_factory=list)

@dataclass_json
@dataclass
class TypeRef:
    typeId: str
    nullable: bool = False

@dataclass_json
@dataclass
class Constraints:
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    pattern: Optional[str] = None

@dataclass_json
@dataclass
class Type:
    id: str
    name: str
    kind: str
    description: Optional[str] = None
    properties: Dict[str, TypeRef] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    items: Optional[TypeRef] = None
    enum: List[Any] = field(default_factory=list)
    oneOf: List[TypeRef] = field(default_factory=list)
    allOf: List[TypeRef] = field(default_factory=list)
    constraints: Optional[Constraints] = None

@dataclass_json
@dataclass
class Body:
    contentTypes: List[str]
    schema_ref: TypeRef

@dataclass_json
@dataclass
class Inputs:
    pathParams: Dict[str, TypeRef] = field(default_factory=dict)
    queryParams: Dict[str, TypeRef] = field(default_factory=dict)
    headers: Dict[str, TypeRef] = field(default_factory=dict)
    body: Optional[Body] = None

@dataclass_json
@dataclass
class Response:
    status: int
    contentTypes: List[str]
    schema_ref: Optional[TypeRef] = None

@dataclass_json
@dataclass
class Outputs:
    success: List[Response] = field(default_factory=list)
    errors: List[Response] = field(default_factory=list)

@dataclass_json
@dataclass
class Pagination:
    mode: str
    request: Dict[str, Any]
    response: Dict[str, Any]

@dataclass_json
@dataclass
class Semantics:
    idempotent: bool = False
    safe: bool = False
    paginated: Optional[Pagination] = None

@dataclass_json
@dataclass
class Operation:
    id: str
    name: str
    transport: str
    method: str
    pathTemplate: str
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    inputs: Inputs = field(default_factory=Inputs)
    outputs: Outputs = field(default_factory=Outputs)
    semantics: Semantics = field(default_factory=Semantics)

@dataclass_json
@dataclass
class IR:
    service: Service
    types: List[Type]
    operations: List[Operation]
    meta: Optional[Meta] = None
    servers: List[Server] = field(default_factory=list)
    securitySchemes: List[SecurityScheme] = field(default_factory=list)

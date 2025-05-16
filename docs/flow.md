```mermaid
sequenceDiagram
    participant Client
    participant Route
    participant Schema
    participant Service
    participant Model

    Client->>Route: POST /auth/login
    Route->>Schema: 校验数据格式
    Schema-->>Route: 校验后的数据
    Route->>Service: 调用认证服务
    Service->>Model: 查询数据库
    Model-->>Service: 返回对象
    Service-->>Schema: 返回对象
    Schema-->>Route: 返回序列化对象
    Route->>Route: 生成JWT令牌
    Route-->>Client: 返回令牌
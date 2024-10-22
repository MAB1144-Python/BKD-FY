
origins = [
    #local v1
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8225",
    "http://127.0.0.1:4200",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

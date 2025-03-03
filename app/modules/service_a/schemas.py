from pydantic import BaseModel, Field

class RequestData(BaseModel):
    name: str = Field(default="Самсон", description="Имя создающего заявку")
    surname: str = Field(default="Самсонов", description="Фамилия создающего заявку")
    reason: str = Field(default="Беды с головой", description="Причина заявки")
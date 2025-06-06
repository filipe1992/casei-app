import logging
from typing import Optional
import httpx
from fastapi import HTTPException
from pydantic import BaseModel

class WhatsAppMessageRequest(BaseModel):
    chatId: str
    text: str
    reply_to: Optional[str] = None
    linkPreview: bool = True
    linkPreviewHighQuality: bool = False
    session: str = "default"

class WhatsAppReactionRequest(BaseModel):
    messageId: str
    reaction: str
    session: str = "default"

class WhatsAppService:
    def __init__(self, base_url: str = "http://waha:3000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def send_message(
        self,
        phone_number: str,
        message: str,
        reply_to: Optional[str] = None,
        link_preview: bool = True,
        link_preview_high_quality: bool = False,
        session: str = "default"
    ) -> dict:
        logging.info(f"Enviando mensagem para {phone_number}: {message}")
        """
        Envia uma mensagem de WhatsApp usando a API WAHA.

        Args:
            phone_number (str): Número do telefone do destinatário (sem o '+' e com código do país)
            message (str): Mensagem a ser enviada
            reply_to (Optional[str], optional): ID da mensagem para responder. Defaults to None.
            link_preview (bool, optional): Ativar preview de links. Defaults to True.
            link_preview_high_quality (bool, optional): Preview de links em alta qualidade. Defaults to False.
            session (str, optional): Sessão do WhatsApp. Defaults to "default".

        Returns:
            dict: Resposta da API do WhatsApp

        Raises:
            HTTPException: Se houver erro na requisição
        """
        # Formata o número do telefone para o formato esperado pelo WAHA
        chat_id = f"{phone_number}@c.us"

        payload = WhatsAppMessageRequest(
            chatId=chat_id,
            text=message,
            reply_to=reply_to,
            linkPreview=link_preview,
            linkPreviewHighQuality=link_preview_high_quality,
            session=session
        )

        try:
            response = await self.client.post(
                f"{self.base_url}/api/sendText",
                json=payload.model_dump()
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar mensagem do WhatsApp: {str(e)}"
            )
        
    async def send_reaction(self, message_id: str, reaction: str, session: str = "default") -> None:
        """
        Envia uma reação para uma mensagem no WhatsApp.
        """
        payload = WhatsAppReactionRequest(
            messageId=message_id,
            reaction=reaction,
            session=session
        )
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/reaction",
                json=payload.model_dump()
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar reação do WhatsApp: {str(e)}"
            )

    async def close(self):
        """Fecha o cliente HTTP assíncrono"""
        await self.client.aclose()

# Instância global do serviço
whatsapp_service = WhatsAppService()

# Função para obter a instância do serviço
def get_whatsapp_service() -> WhatsAppService:
    return whatsapp_service 
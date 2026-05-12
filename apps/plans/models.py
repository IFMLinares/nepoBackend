from django.db import models
from apps.common.models import TimestampedModel

class Plan(TimestampedModel):
    """
    Representa los diferentes planes de suscripción o cursos disponibles.
    """
    name = models.CharField(max_length=255, verbose_name="Nombre del Plan")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    strikethrough_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        default=0, 
        verbose_name="Precio Tachado"
    )
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_promotion = models.BooleanField(default=False, verbose_name="¿Es Promoción?")
    requires_inscription = models.BooleanField(default=False, verbose_name="Requiere Inscripción")
    is_active = models.BooleanField(default=True, verbose_name="Está Activo")

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"
        ordering = ['price']

    def __str__(self) -> str:
        return self.name

class PlanFeature(TimestampedModel):
    """
    Características específicas incluidas o no en un plan (Check/Cancel).
    """
    plan = models.ForeignKey(
        Plan, 
        related_name='features', 
        on_delete=models.CASCADE, 
        verbose_name="Plan"
    )
    description = models.CharField(max_length=255, verbose_name="Descripción de la Característica")
    is_included = models.BooleanField(default=True, verbose_name="¿Incluido?")

    class Meta:
        verbose_name = "Característica de Plan"
        verbose_name_plural = "Características de Planes"

    def __str__(self) -> str:
        prefix = "✔" if self.is_included else "✘"
        return f"{prefix} {self.description} ({self.plan.name})"

class Requirement(TimestampedModel):
    """
    Bloques informativos de requisitos para la academia (texto, viñetas o Markdown).
    """
    title = models.CharField(max_length=255, verbose_name="Título del Requisito")
    content = models.TextField(verbose_name="Contenido (Soporta Markdown)")
    is_active = models.BooleanField(default=True, verbose_name="Está Activo")

    class Meta:
        verbose_name = "Requisito"
        verbose_name_plural = "Requisitos"

    def __str__(self) -> str:
        return self.title

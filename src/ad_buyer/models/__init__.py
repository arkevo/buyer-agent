# Author: Green Mountain Systems AI Inc.
# Donated to IAB Tech Lab

"""Data models for the Ad Buyer System."""

from .opendirect import (
    Account,
    Creative,
    Line,
    LineBookingStatus,
    Order,
    OrderStatus,
    Organization,
    Product,
    RateType,
)
from .flow_state import BookingState
from .buyer_identity import (
    AccessTier,
    BuyerContext,
    BuyerIdentity,
    DealRequest,
    DealResponse,
    DealType,
)
from .ucp import (
    AudienceCapability,
    AudiencePlan,
    AudienceValidationResult,
    CoverageEstimate,
    EmbeddingType,
    SignalType,
    SimilarityMetric,
    UCPConsent,
    UCPContextDescriptor,
    UCPEmbedding,
    UCPModelDescriptor,
)
from .deals import (
    AvailabilityInfo,
    BuyerIdentityPayload,
    DealBookingRequest,
    OpenRTBParams,
    PricingInfo,
    ProductInfo,
    QuoteRequest,
    QuoteResponse,
    SellerErrorResponse,
    TermsInfo,
)
# Avoid shadowing buyer_identity.DealResponse with deals.DealResponse
# by importing the deals version under a distinct name
from .deals import DealResponse as SellerDealResponse

__all__ = [
    # OpenDirect models
    "Account",
    "Creative",
    "Line",
    "LineBookingStatus",
    "Order",
    "OrderStatus",
    "Organization",
    "Product",
    "RateType",
    # Flow state models
    "BookingState",
    # Buyer identity models
    "AccessTier",
    "BuyerContext",
    "BuyerIdentity",
    "DealRequest",
    "DealResponse",
    "DealType",
    # UCP models
    "AudienceCapability",
    "AudiencePlan",
    "AudienceValidationResult",
    "CoverageEstimate",
    "EmbeddingType",
    "SignalType",
    "SimilarityMetric",
    "UCPConsent",
    "UCPContextDescriptor",
    "UCPEmbedding",
    "UCPModelDescriptor",
    # Deals API v1.0 models (quote-then-book)
    "AvailabilityInfo",
    "BuyerIdentityPayload",
    "DealBookingRequest",
    "OpenRTBParams",
    "PricingInfo",
    "ProductInfo",
    "QuoteRequest",
    "QuoteResponse",
    "SellerDealResponse",
    "SellerErrorResponse",
    "TermsInfo",
]

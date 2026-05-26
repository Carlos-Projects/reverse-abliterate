ABLITERATION_META_FILE = "abliteration_metadata.json"
OBLITERATED_SUFFIX = "-OBLITERATED"
COMMIT_PATTERN = "OBLITERATUS: abliterated"
LORA_FILES = {"adapter_config.json", "adapter_model.safetensors"}

SUSPICIOUS_LAYER_NAMES = [
    "self_attn.q_proj.weight",
    "self_attn.k_proj.weight",
    "self_attn.v_proj.weight",
    "self_attn.o_proj.weight",
    "mlp.gate_proj.weight",
    "mlp.up_proj.weight",
    "mlp.down_proj.weight",
    "input_layernorm.weight",
    "post_attention_layernorm.weight",
]

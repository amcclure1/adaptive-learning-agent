# Hermes v0.18.2 Static-Asset Presentation Investigation

Status: Complete for the pinned Windows CLI/plugin boundary; real study acceptance remains blocked on human pack approval  
Investigated: 2026-07-18

## Pinned identity

The installed isolated runtime reports:

- package: `hermes-agent` 0.18.2;
- release date identifier: `2026.7.7.2`;
- executable banner: `Hermes Agent v0.18.2 (2026.7.7.2)`;
- Python: 3.13.14.

The matching official source tag is [`v2026.7.7.2`](https://github.com/NousResearch/hermes-agent/tree/v2026.7.7.2), not `v0.18.2`. The annotated tag object is `b7751df34688835a108e0d630f3495fc11f3df79` and points to release commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`, whose release message identifies Hermes Agent v0.18.2.

## Tagged public plugin boundary

The tagged [plugin guide](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/website/docs/user-guide/features/plugins.md) demonstrates custom tools whose handlers return `json.dumps(...)`. The tagged [`tools/registry.py`](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/tools/registry.py) states that every tool handler must return a JSON string. The tagged [`PluginContext.register_tool`](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/hermes_cli/plugins.py) accepts a schema and handler but exposes no documented result renderer or local-image attachment parameter.

Actual runtime introspection of `PluginContext` found no image/media/attachment/send method. Its only image-named registration method is `register_image_gen_provider`, which is a provider backend surface for image generation, not a way for an ordinary custom tool to display an existing local PNG to the CLI learner.

## Tagged vision boundary

The tagged [Vision & Image Paste guide](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/website/docs/user-guide/features/vision.md) documents user-to-model image input from clipboard/paste and provider routing. It also documents internal multimodal results for the built-in `vision_analyze` flow. It does not document an ordinary custom-plugin tool returning an existing local image as learner-facing CLI output.

Tagged internals contain a private `_multimodal` envelope used to carry image content to a compatible model. That is not the public JSON-string plugin contract, is not a learner-facing terminal renderer, and would route pixels into model vision—the opposite of this project's no-model-interpretation boundary. It is therefore not used.

## Determination

For pinned Hermes v0.18.2 Windows CLI, a supported public custom-plugin mechanism for learner-facing local-image output is **unsupported**. The implemented integration remains thin:

1. the core returns a digest-bound logical asset descriptor;
2. the ordinary Hermes tool handler returns JSON as documented;
3. the skill presents the approved caption, alt text, and terminal fallback before showing options;
4. the skill requires explicit access confirmation before soliciting an answer;
5. no Hermes core/configuration change, model vision, arbitrary local path, binary JSON, or unsupported multimodal envelope is used.

This establishes the fallback choice. It does not claim that every Hermes gateway surface lacks attachment support, nor does it complete real Hermes E7B acceptance. That acceptance must wait for explicit human pack approval.

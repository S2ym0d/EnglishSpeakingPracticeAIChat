import requests

def ollama_generate(prompt, model, url, timeout):
    try:
        resp = requests.post(url, json = {"model": model, "prompt": prompt, "stream": False}, timeout = timeout)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict) and "response" in data:
            return data["response"]
        # end if

        if isinstance(data, dict) and "results" in data:
            texts = []
            for r in data["results"]:
                if isinstance(r, dict) and "contents" in r:
                    for c in r["contents"]:
                        if c.get("type") == "output_text":
                            texts.append(c.get("text", ""))
                        # end if
                    # end for
                # end if
            # end for
            return "\n".join(texts).strip()
        # end if

        return str(data)
    except Exception as exc:
        raise RuntimeError(f"Ollama request failed: {exc}")
    # end try
# end def

def ollama_chat(messages, model, url, timeout):
    try:
        resp = requests.post(url, json = {"model": model, "messages": messages, "stream": False}, timeout = timeout)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict) and "message" in data:
            msg = data["message"]
            
            if isinstance(msg, dict) and "content" in msg:
                return msg["content"]
            # enf if

            return str(msg)
        # end if

        if isinstance(data, dict) and "response" in data:
            return data["response"]
        # end if

        if isinstance(data, dict) and "results" in data:
            texts = []
            for r in data["results"]:
                if isinstance(r, dict) and "contents" in r:
                    for c in r["contents"]:
                        if c.get("type") == "output_text":
                            texts.append(c.get("text", ""))
                        # end if
                    # end for
                # end if
            # end for
            return "\n".join(texts).strip()
        # end if

        return str(data)
    except Exception as exc:
        raise RuntimeError(f"Ollama request failed: {exc}")
    # end try
# end def
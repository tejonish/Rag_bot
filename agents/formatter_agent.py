def format_output(matched, partial, missing, score, coverage):

    result = f"🎯 Fit Score: {score}\n\n"

    result += "✅ Matching Skills:\n"
    result += "\n".join(f"- {s}" for s in matched) if matched else "- None"

    result += "\n\n⚠️ Partially Matching Skills:\n"
    result += "\n".join(f"- {s}" for s in partial) if partial else "- None"

    result += "\n\n❌ Missing Skills:\n"
    result += "\n".join(f"- {s}" for s in missing) if missing else "- None"

    result += f"\n\n📄 Keyword Coverage: {coverage}%\n"

    return result

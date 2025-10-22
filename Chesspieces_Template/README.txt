English Translation:

Instructions:
Open the images in "swap_body" with an image editor (preferably one that supports working with layers), then load the sprite of the desired statue and adjust it to the same position as the template. It's not necessary for the size to be the same as the template's; it is only necessary for the size of the new statue to be consistent across all 3 images. Follow these definitions for guidance:
swap_body-1: When the player moves forward and the camera sees their back.
swap_body-2: When the player moves backward and the camera sees their face.
swap_body-3: When the player moves right, the sprite flips (or is mirrored) when the player moves left.
When you have the images ready, save them with the same name and the same dimensions, as a 32-bit depth png, in a folder named "swap-body," then place that folder alongside the "swap" SCML file. The SCML file should not be modified.

IMPORTANT: The same SCML can be used for all pieces; only the name of the .scml file must be changed to match the name and material of the piece being built.

---

手順:
まず、「swap_body」内の画像を画像編集ソフト（できればレイヤー機能に対応したもの）で開き、使用したい像（スタチュー）の**スプライト**を読み込みます。そのスプライトを、テンプレート画像と同じ位置に調整してください。
サイズはテンプレートと完全に一致させる必要はありません。**新しい像のサイズが、3枚の画像すべてで一貫していること**が重要です。

以下の定義を参考に、画像を調整してください。
swap_body-1: プレイヤーが**前進**している時、カメラが**背面**を見るアングル。
swap_body-2: プレイヤーが**後退**している時、カメラが**正面（顔）**を見るアングル。
swap_body-3: プレイヤーが**右に移動**している時の画像。プレイヤーが**左に移動**する際は、このスプライトを**反転（ミラーリング）**して使用します。

画像が準備できたら、元の画像と**同じ名前**、**同じ寸法**で、**32ビット深度のPNG**ファイルとして、「**swap-body**」という名前のフォルダに保存してください。
この「swap-body」フォルダを、「swap」SCMLファイルと同じ階層に配置します。**SCMLファイル自体は変更する必要はありません。**

**重要:**
すべてのパーツに**同じSCML**ファイルを使用できます。ただし、**構築するパーツの名前と素材**に合わせて、**.scmlファイルの名前だけは変更**してください。
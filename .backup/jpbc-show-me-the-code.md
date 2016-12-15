---
title: JPBC(Java Pairing Based Cryptography) 库 实例详解
comments: true
categories: Java
toc: true
tags:
	- JPBC
	- Cryptography
	- 密码学
---


### 前言:

前面一篇文章讲了JPBC库的基本使用，但是单单一个介绍可能还是很难知道如何去实践，我这里把我最近实现的一个论文里的算法给拿过来，作为实例进行解释如何使用JPBC。
<!-- more -->
论文地址: [可证安全的高效可托管公钥加密方案_刘文浩](https://joway.wang/assets/files/可证安全的高效可托管公钥加密方案_刘文浩.pdf)

代码下载: [JPBC_Optimize_IBE](https://github.com/joway/JPBC_Optimize_IBE)

该方案是对 BF-IBE 方案 的一种改进，实现可托管加解密。生成一个公钥，一个托管私钥，一个主私钥，主私钥包含数字签名功能。

### 建立Model

#### CommonText

``` java
public interface CommonText extends Externalizable {
    /*
    由于jpbc库的Element类型不支持序列化, 所以使用这个java原生的自定义序列化接口,
    来达到序列化的目的.
     */
    String toString();
}
```

实现Externalizable接口，为了能够序列为比特流存入文件中。

#### CipherText

``` java
public class CipherText implements CommonText {
    private Element U;

    private ArrayList<byte[]> V;
    
    ...
}
```

U 为密文标识，V 为 经国处理后的密文二进制流

#### PlainText
 
``` java
public class PlainText implements CommonText {
    private ArrayList<byte[]> message;
    ...
}
```

#### UserKey

``` java
public class UserKey {
    // 以下为用户私有信息
    private Element Kp; // 主解密私钥
    private Element Ke; // 托管私钥,交给服务器
    private Element Ppub; // 公钥


    public UserKey() {
    }
}
```
#### SystemParameter

``` java
public class SystemParameter {



    // 系统公共参数:
    // 1. 素数阶q
    // 2. G1,G2, 其中G2 == G1
    private Field G1;

    // 3. 双线性映射关系 e ( 这里设成pairing
    /*
    pairing.pairing(x, y) 代表数学上 e（x,y）
    双线性映射
    */
    private static Pairing pairing;

    // 4. n : 二进制位数

    // 5. P : 群G1的生成元
    private Element P;// G1的生成元

    // 6. g2 : e(P,P) 值
    private Element g2;

    // 7. H : 杂凑函数(这里选择哈希函数 sh256)


    public static int SIZE = 32; // 256 bit

    public SystemParameter(Field g1, Pairing pairing, Element p, Element g2, Field zr) {
        G1 = g1;
        SystemParameter.pairing = pairing;
        P = p;
        this.g2 = g2;
        Zr = zr;

    }


    public Field getZr() {
        return Zr;
    }

    public void setZr(Field zr) {
        Zr = zr;
    }

    private Field Zr; // // {1,...,r} 整数集


    public SystemParameter(Field g1, Pairing pairing, Element p, Element g2) {
        G1 = g1;
        this.pairing = pairing;
        P = p;
        this.g2 = g2;
    }
    
    ....

}

```

### 基础加解密实现:

详情见注释

### Ident 接口

之所以弄个接口，是为了后面测试性能的时候，可以用到代理，这样方便点。

``` java
public interface Ident {

    void setUp();

    UserKey privateKeyGen();

    CipherText encrypt(PlainText plainText, UserKey userKey);
    CipherText encrypt(String filename, UserKey userKey) throws IOException;

    PlainText userDecrypt(CipherText cipherText, UserKey userKey);

    PlainText escrowDecrypt(CipherText cipherText, UserKey userKey);

    PlainText userDecrypt(String filename, UserKey userKey) throws IOException, ClassNotFoundException;

    PlainText escrowDecrypt(String filename, UserKey userKey) throws IOException, ClassNotFoundException;
}
```

### BaseIdentSystem

该类实现了:

- 系统初始化
- 密钥生成
- 加密文件或比特流
- 用户主私钥解密文件或比特流
- 托管解密主私钥或比特流

``` java
public class BaseIdentSystem implements Ident {

    private SystemParameter systemParameter;


    public BaseIdentSystem() {
        setUp();
    }

    /**
     * 判断配对是否为对称配对，不对称则输出错误信息
     *
     * @param pairing
     */
    private void checkSymmetric(Pairing pairing) {
        if (!pairing.isSymmetric()) {
            throw new RuntimeException("密钥不对称!");
        }
    }


    /*只需要启动一次
    系统初始化(Setup): 给定一个安全参数k,执行下面的步骤。
    1) 输出 2 个阶为素数 q 的循环群 G1 与 G2 、群G1的生成元P,以及双线性映射e:G1 X G1 ->G2
    2)计算g2 = e(P,P)。
    3)选择杂凑函数H:G2 -> {0,1}^n,其中n是整数。
    此方案的明文空间是 M = {0,1}^n ,密文空间是 C = G^* X {0,1}^n。
    系统公共参数 params 为 (q,G1,G2,e,n,P,g2,H)。
     */
    @Override
    public void setUp() {
        Utils.log("-------------------系统建立阶段----------------------");
        //双线性群的初始化
        Pairing pairing = PairingFactory.getPairing("jpbc.properties");
        PairingFactory.getInstance().setUsePBCWhenPossible(true);
        checkSymmetric(pairing);

        Field G1 = pairing.getG1(); //G1 == G2 对称

        Element P = G1.newRandomElement().getImmutable();// 生成G1的生成元P

        Element g2 = pairing.pairing(P, P).getImmutable();

        systemParameter = new SystemParameter(
                G1, pairing, P, g2, pairing.getZr()
        );
    }


    /*用户的(双)私钥生成算法:每个用户生成自己的公钥及其对应的 2 个 解密私钥。
    1. 随机选择一个随机数 x (- Zq ,并将其 设置为主解密私钥,即Kp = x。
    2. 将托管解密私钥设为Ke = x^-1 P
    3. 将公钥设为Ppub = xP (- G1 。
     */
    @Override
    public UserKey privateKeyGen() {
        Utils.log("-------------------密钥生成阶段----------------------");
        Element x = getRandInZr(); // 用户自己主私钥,用户自己设置

        Element Kp = x.getImmutable();
        Element Ke = systemParameter.getP().mulZn(x.invert()).getImmutable();
        Element Ppub = systemParameter.getP().mulZn(x).getImmutable();

        return new UserKey(Kp, Ke, Ppub);
    }

    /*
    拿Ppub对V加密
    密文 C = (U, V)
    1. 首先选择 r (- Zq
    2.
     */
    @Override
    public CipherText encrypt(PlainText plainText, UserKey userKey) {
        Utils.log("-------------------加密阶段----------------------");
        Element r = getRandInZr();
        Element U = userKey.getPpub().mulZn(r).getImmutable();//U

        Element g2_r = systemParameter.get_g2().powZn(r);
        byte[] sha256_g2_r = Utils.sha256(g2_r.toBytes());

        ArrayList<byte[]> cipherV = new ArrayList<>();
        int size = plainText.getMessage().size();
        ArrayList<byte[]> bytesBox = plainText.getMessage();

        for (int i = 0; i < size; ++i) {
            cipherV.add(Utils.xor(bytesBox.get(i), sha256_g2_r));
        }

        Utils.log("明文", plainText);
        Utils.log("密文", new CipherText(U, cipherV));
        return new CipherText(U, cipherV);
    }

    @Override
    public CipherText encrypt(String filename, UserKey userKey) throws IOException {
        return encrypt(new PlainText(FileUtils.fileToByteArray(filename)), userKey);
    }


    /*
    拿Ke对V解密
     */
    @Override
    public PlainText userDecrypt(CipherText cipherText, UserKey userKey) {
        Utils.log("-------------------主私钥解密阶段----------------------");

        Utils.logBegTime();
        Element eUKp_1_P = pairing(
                cipherText.getU().getImmutable(),
                systemParameter.getP().mulZn(userKey.getKp().invert())).getImmutable();
        Utils.logEndTime("配对结束");

        ArrayList<byte[]> plainBytes = new ArrayList<>();
        ArrayList<byte[]> cipherV = cipherText.getV();

        Utils.logBegTime();
        byte[] sha256_eUKp_1_P = Utils.sha256(eUKp_1_P.toBytes());
        Utils.logEndTime("哈希结束");

        Utils.logBegTime();
        for (byte[] aCipherV : cipherV) {
            plainBytes.add(Utils.xor(aCipherV,sha256_eUKp_1_P));
        }
        Utils.logEndTime("解密异或循环结束");


        Utils.log("主私钥解密后明文", new PlainText(plainBytes));
        return new PlainText(plainBytes);
    }

    @Override
    public PlainText userDecrypt(String filename, UserKey userKey)
            throws ClassNotFoundException, IOException {
        Utils.logBegTime();
        CipherText cipherText = (CipherText) FileUtils.readObject(filename);
        Utils.logEndTime("读取密文文件中的信息至内存");
        return userDecrypt(cipherText, userKey);
    }

    @Override
    public PlainText escrowDecrypt(CipherText cipherText, UserKey userKey) {
        Utils.log("-------------------托管私钥解密阶段----------------------");

        Element eUKe = pairing(
                cipherText.getU().getImmutable(),
                userKey.getKe().getImmutable()).getImmutable();

        byte[] sha256_eUKe = Utils.sha256(eUKe.toBytes());

        ArrayList<byte[]> plainBytes = new ArrayList<>();
        ArrayList<byte[]> cipherV = cipherText.getV();

        for (byte[] aCipherV : cipherV) {
            plainBytes.add(Utils.xor(aCipherV, sha256_eUKe));
        }

        Utils.log("托管解密后明文", new PlainText(plainBytes));
        return new PlainText(plainBytes);
    }

    // BLS sing:




    @Override
    public PlainText escrowDecrypt(String filename, UserKey userKey) throws IOException, ClassNotFoundException {
        CipherText cipherText = (CipherText) FileUtils.readObject(filename);
        return escrowDecrypt(cipherText, userKey);
    }

    private Element getRandInZr() {
        return systemParameter.getZr().newRandomElement().getImmutable();
    }

    private Element pairing(Element var1, Element var2) {
        return SystemParameter.getPairing().pairing(var1, var2).getImmutable();
    }

}
```

#### BLS 短签名:

用于对用户加密后的文件进行签名认证

``` java
public class BLS01 {

    public BLS01() {

    }

    public BLS01Parameters setup() {
        BLS01ParametersGenerator setup = new BLS01ParametersGenerator();
        setup.init(PairingFactory.getPairingParameters("jpbc.properties"));

        return setup.generateParameters();
    }

    public AsymmetricCipherKeyPair keyGen(BLS01Parameters parameters) {
        BLS01KeyPairGenerator keyGen = new BLS01KeyPairGenerator();
        keyGen.init(new BLS01KeyGenerationParameters(null, parameters));

        return keyGen.generateKeyPair();
    }

    public byte[] sign(String message, CipherParameters privateKey) {
        byte[] bytes = message.getBytes();

        BLS01Signer signer = new BLS01Signer(new SHA256Digest());
        signer.init(true, privateKey);
        signer.update(bytes, 0, bytes.length);

        byte[] signature = null;
        try {
            signature = signer.generateSignature();
        } catch (CryptoException e) {
            throw new RuntimeException(e);
        }
        return signature;
    }

    public boolean verify(byte[] signature, String message, CipherParameters publicKey) {
        byte[] bytes = message.getBytes();

        BLS01Signer signer = new BLS01Signer(new SHA256Digest());
        signer.init(false, publicKey);
        signer.update(bytes, 0, bytes.length);

        return signer.verifySignature(signature);
    }

    public static void main(String[] args) {
        BLS01 bls01 = new BLS01();

        // Setup
        AsymmetricCipherKeyPair keyPair = bls01.keyGen(bls01.setup());

        // Test same message
        String message = "Hello World!";

        System.out.println(bls01.sign(message, keyPair.getPrivate()).length);

        assertTrue(bls01.verify(bls01.sign(message, keyPair.getPrivate()), message, keyPair.getPublic()));

        // Test different messages
        assertFalse(bls01.verify(bls01.sign(message, keyPair.getPrivate()), "Hello Italy!", keyPair.getPublic()));
    }

}
```